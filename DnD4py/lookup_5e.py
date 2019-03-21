#!/usr/bin/env python
from bs4 import BeautifulSoup as bs
import requests
import argparse
from textwrap import fill as wrap

__all__ = ['Roll20', 'Roll20Monster', 'Roll20Spell', 'Roll20Item']


def stringify(text):
    text = text.replace('<br>', '\n').replace('<br />', '\n')
    text = text.replace('<h2>', '*').replace('</h2>', '*\n')
    text = text.replace('<strong>', '').replace('</strong>', '')
    return wrap(text, 70, drop_whitespace=False, replace_whitespace=False)


def score_to_mod(score):
    return '{:+d}'.format((score - 10)//2)


class Roll20:
    
    def __init__(self, name, site='https://roll20.net/compendium/dnd5e/'):
        self.name = name.rstrip().title()
        formatted_name = self.name.replace(' ', '_')
        url = site + formatted_name
        page = requests.get(url)
        if page.status_code != 200:
            raise IOError('{:s} not found at {:s}.'.format(name,
                                                           url))
        if 'marketplace' in page.url:
              raise IOError('{:s} not found at {:s}, '
                            'likely because this content is behind a paywall. '
                            'Encourage developer to add alternative back-ends to Roll20'.format(name, url))
        html = page.text
        soup = bs(html, 'html.parser')
        self.attributes = ({stringify(a.text):
                            stringify(a.find_next(attrs={'class':
                                                         'value'}).text)
                            for a in soup.find_all(attrs={'class':
                                                          'col-md-3 attrName'})})
        self.desc = '\n'.join([stringify(val.text)
                               for val in soup.find_all(id='origpagecontent',
                                                        attrs={'type':
                                                               'text/html'})])
        
    def get(self, key, alt=None):
        if key == 'desc':
            return self.desc or alt
        else:
            return self.attributes.get(key, alt)
            
    @property
    def str_attributes(self):
        res = ""
        for k, v in self.attributes.items():
            res += k + ': ' + v + '\n'
        return res
        
    @property
    def str_desc(self):
        res = '\n\nDescription\n===========================\n' + self.desc
        return res
        
    def __len__(self):
        return len(self.attributes)
        
    def __str__(self):
        return self.name + '\n\n' + self.str_attributes + self.str_desc

    @property
    def as_unicode(self):
        return self.__str__().encode('utf-8')
    

class Roll20Monster(Roll20):
    
    def __init__(self, name,
                 site='https://roll20.net/compendium/dnd5e/Monsters:'):
        Roll20.__init__(self, name, site=site)
                
    @property
    def str_attributes(self):
        res = ''
        for k in ['HP', 'AC', 'Speed', 'Challenge Rating']:
            res += k + ': ' + self.get(k, 'EMPTY') + '\n'
        res += '\n'
        for k in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
            res += k + '\t'
        res += '\n'
        for k in ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']:
            s = self.get(k, None)
            res += '{:s} ({:s})\t'.format(s, score_to_mod(int(s)))
        res += '\n\n'
        for k in ['Type', 'Size', 'Alignment', 'Senses', 'Skills',
                  'Languages']:
            res += k + ': ' + self.get(k, 'EMPTY') + '\n'
        return res


class Roll20Spell(Roll20):
    def __init__(self, name,
                 site='https://roll20.net/compendium/dnd5e/Spells:'):
        Roll20.__init__(self, name, site=site)
                                        
    @property
    def str_attributes(self):
        res = ''
        for k in ['Level', 'School', 'Classes']:
            if self.get(k) is not None:
                res += k + ': ' + self.get(k, 'EMPTY') + '\n'
        res += '\n'
        for k in ['Casting Time', 'Duration', 'Concentration', 'Ritual',
                  'Components', 'Material']:
            if self.get(k) is not None:
                res += k + ': ' + self.get(k, 'EMPTY') + '\n'
        res += '\n'
        for k in ['Range', 'Damage', 'Damage Type', 'Save', 'Target']:
            if self.get(k) is not None:
                res += k + ': ' + self.get(k, 'EMPTY') + '\n'
        return res

    def as_dungeonsheets_class(self):
        spell_name = self.name
        class_name = spell_name.replace(' ', '').replace('-', '')
        res = 'class {:s}(Spell):\n'.format(class_name)
        res += "    \"\"\"{:s}\n    \"\"\"\n".format(self.desc.replace('\n', '\n    '))
        res += "    name = \"{:s}\"\n".format(spell_name)
        res += "    level = {:d}\n".format(int(self.get('Level', -1)))
        res += "    casting_time = \"{:s}\"\n".format(self.get('Casting Time', '1 action'))
        res += "    casting_range = \"{:s}\"\n".format(self.get('Range', ''))
        str_components = self.get('Components', '').upper().split(' ')
        if len(str_components) == 0:
            res += "    components = ()\n"
        else:
            res += "    components = {:s}\n".format(str(tuple(str_components)))
        res += "    materials = \"\"\"{:s}\"\"\"\n".format(self.get('Material', ''))
        dur_text = "\"{:s}\"\n".format(self.get('Duration', 'Instantaneous'))
        dur_text = ("\"Concentration, {:s}".format(dur_text.lstrip('\"')) if
                    self.get('Concentration', '') else dur_text)
        duration = "    duration = " + dur_text
        res += duration
        res += "    ritual = {:}\n".format(bool(self.get('Ritual', '')))
        res += "    magic_school = \"{:s}\"\n".format(self.get('School', ''))
        res += "    classes = {:s}\n".format(str(tuple(self.get('Classes', '').split(', '))))
        return res + "\n"


class DnDSpell(Roll20Spell):
    def __init__(self, name, site="https://www.dnd-spells.com/spell/"):
        self.name = name.rstrip().title()
        self.attributes = {'Ritual': False}
        formatted_name = self.name.lower().replace(' ', '-')
        url = site + formatted_name
        page = requests.get(url, timeout=2)
        if (page.status_code != 200) or (page.url != url):
            url_other = url + '-ritual'
            page = requests.get(url_other, timeout=2)
            if (page.status_code != 200) or (page.url != url_other):
                raise IOError('{:s} not found at {:s}.'.format(name,
                                                               url))
            self.attributes['Ritual'] = True
        soup = bs(page.text, 'html.parser')
        base = soup.find_all('h1')[0]
        school = base.find_next('p')
        self.attributes['School'] = school.text
        body = school.find_next('p')
        details = body.text.strip().replace('\r', '').replace('\n', '').split('                 ')
        for entry in details:
            k, v = entry.split(': ')
            self.attributes[k.title()] = v.capitalize()
        if '(' in self.attributes['Components']:
            self.attributes['Components'], mat = self.attributes['Components'].split('(')
            self.attributes['Material'] = mat.strip(')').capitalize()

        self.attributes['Components'] = self.attributes['Components'].replace(' ', '').replace(',', ' ')
        if 'cantrip' in self.attributes['Level'].lower():
            self.attributes['Level'] = '0'
        desc = body.find_next('p')
        self.desc = desc.text.strip().replace('\r', '')
        if 'higher level' in desc.find_next('h4').text.lower():
            desc = desc.find_next('p')
            self.desc += '\n\nAt Higher Levels: '
            self.desc += desc.text.strip()
        self.desc = wrap(self.desc, 80, drop_whitespace=False,
                        replace_whitespace=False)
        classes = desc.find_next('p').find_next('p')
        self.attributes['Classes'] = ', '.join(classes.text.replace(',', '').split()[1:-1])
    
class Roll20Item(Roll20):
    def __init__(self, name,
                 site='https://roll20.net/compendium/dnd5e/Items:'):
        Roll20.__init__(self, name, site=site)

    def as_dungeonsheets_class(self):
        spell_name = self.name
        class_name = spell_name.replace(' ', '')
        res = 'class {:s}(MagicItem):\n'.format(class_name)
        res += "    \"\"\"{:s}\n    \"\"\"\n".format(self.desc.replace('\n', '\n    '))
        res += "    name = \"{:s}\"\n".format(spell_name)
        return res + "\n"

def monster_lookup():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            """Searches Roll20.net 5e monster compendium for the term queried."""))
    parser.add_argument('query', nargs='+', help='The words to search')

    args = parser.parse_args()
    text = ' '.join(args.query)

    try:
        item = Roll20Monster(text)
    except IOError as e:
        print(e)
        item = None
    if item is None or len(item) == 0:
        return False
    else:
        try:
            print(item)
        except UnicodeEncodeError:
            print(item.as_unicode)
        return True
    
    
def spell_lookup():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            """Searches Roll20.net 5e Spell compendium for the term queried."""))
    parser.add_argument('--ds',
                        help='Parse as dungeonsheets class', action='store_true')
    parser.add_argument('query', nargs='+', help='The words to search')

    args = parser.parse_args()
    text = ' '.join(args.query)
    
    try:
        item = DnDSpell(text)
#         item = Roll20Spell(text)
    except IOError as e:
        print(e)
        item = None
    if item is None or len(item) == 0:
        return False
    else:
        try:
            if args.ds:
                print(item.as_dungeonsheets_class())
            else:
                print(item)
        except UnicodeEncodeError:
            print(item.as_unicode)
        return True

    
def item_lookup():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            """Searches Roll20.net 5e Item compendium for the term queried."""))
    parser.add_argument('query', nargs='+', help='The words to search')

    args = parser.parse_args()
    text = ' '.join(args.query)
    
    try:
        item = Roll20Item(text)
    except IOError as e:
        print(e)
        item = None
    if item is None or len(item) == 0:
        return False
    else:
        try:
            print(item)
        except UnicodeEncodeError:
            print(item.as_unicode)
        return True


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            """Searches Roll20.net 5e compendium for the term queried."""))

    parser.add_argument('--monster',
                        help='Search only monster lists', action='store_true')
    parser.add_argument('--spell',
                        help='Search only spell lists', action='store_true')
    parser.add_argument('--item',
                        help='Search only item lists', action='store_true')
    parser.add_argument('query', nargs='+', help='The words to search')

    args = parser.parse_args()
    text = ' '.join(args.query)

    item = None
    if args.monster:
        item = Roll20Monster(text)
    elif args.spell:
        item = Roll20Spell(text)
    elif args.item:
        item = Roll20Item(text)
    else:
        for r in [Roll20Monster, Roll20Spell,
                  Roll20Item, Roll20]:
            try:
                item = r(text)
            except IOError as e:
                continue
            else:
                break
    if item is None or len(item) == 0:
        print('Not Found')
    else:
        try:
            print(item)
        except UnicodeEncodeError:
            print(item.as_unicode)
 
        
if __name__ == '__main__':
    main()

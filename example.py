from dataclasses import dataclass

class Namespace:
    def __init__(self):
        self.names = {}

    def add_name(self, name, item):
        self.names[name] = item

    def get_name(self, name):
        if '.' in name:
            name, tail = name.split('.', 1)
            return self.names[name].get_name(tail)
        else:
            return self.names[name]

class Environment(Namespace):
    pass

@dataclass
class Table:
    columns: tuple
    data: list

    def __iter__(self):
        return iter(self.data)

@dataclass
class Import:
    source: str
    destination_space: str
    destination_name: str

    def execute(self, environ):
        destination_space = environ.get_name(self.destination_space)
        with open(self.source) as f:
            data = [tuple(x.strip() for x in row.split(',')) for row in f]
        destination_space.add_name(self.destination_name, Table(data[0], data[1:]))

@dataclass
class Select:
    columns: [str]
    source: str
    condition: (str, str)
    destination_space: str
    destination_name: str

    def execute(self, environ):
        destination_space = environ.get_name(self.destination_space)

        source_table = environ.get_name(self.source)
        indices = [source_table.columns.index(c) for c in self.columns]
        icond = source_table.columns.index(self.condition[0])

        data = [tuple(row[i] for i in indices)
                for row in source_table
                if row[icond] == self.condition[1]
                ]
        destination_space.add_name(self.destination_name, Table(self.columns, data))

@dataclass
class Print:
    source: str

    def execute(self, environ):
        source_table = environ.get_name(self.source)
        col_len = [max(len(c), max((len(str(row[i])) for row in source_table.data), default=0))
                   for i, c in enumerate(source_table.columns)]
        print('='.join('='*x for x in col_len))
        print(' '.join(c.ljust(l) for c, l in zip(source_table.columns, col_len)))
        print(' '.join('-'*x for x in col_len))
        for row in source_table:
            print(' '.join(str(x).ljust(l) for x, l in zip(row, col_len)))
        print('='.join('='*x for x in col_len))

def main():
    tasks = [
        Import('countries.csv', 'work', 'countries'),
        Select(['name', 'capital'], 'work.countries',  ('continent', 'Europe'), 'work', 'european'),
        Print('work.european')
    ]

    environ = Environment()
    environ.add_name('work', Namespace())
    for task in tasks:
        task.execute(environ)

if __name__ == '__main__':
    main()

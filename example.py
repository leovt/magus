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
    def save_as(self, destination, item):
        destination_space, destination_name = destination.rsplit('.', 1)
        self.get_name(destination_space).add_name(destination_name, item)

    def execute(self, task_name, task_arguments):
        dispatcher = {
            'Print': execute_print,
            'Import': execute_import,
            'Select': execute_select,
        }
        execute_task = dispatcher[task_name]
        execute_task(self, task_arguments)


@dataclass
class Table:
    columns: tuple
    data: list

    def __iter__(self):
        return iter(self.data)

@dataclass
class Import:
    source: str
    destination: str

def execute_import(environ, args: Import):
    with open(args.source) as f:
        data = [tuple(x.strip() for x in row.split(',')) for row in f]
    environ.save_as(args.destination, Table(data[0], data[1:]))

@dataclass
class Select:
    columns: [str]
    source: str
    condition: (str, str)
    destination: str

def execute_select(environ, args: Select):
    source_table = environ.get_name(args.source)
    indices = [source_table.columns.index(c) for c in args.columns]
    icond = source_table.columns.index(args.condition[0])

    data = [tuple(row[i] for i in indices)
            for row in source_table
            if row[icond] == args.condition[1]
            ]
    environ.save_as(args.destination, Table(args.columns, data))

@dataclass
class Print:
    source: str

def execute_print(environ, args: Print):
    source_table = environ.get_name(args.source)
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
        Import('countries.csv', 'work.countries'),
        Select(['name', 'capital'], 'work.countries',  ('continent', 'Europe'), 'work.european'),
        Print('work.european')
    ]

    environ = Environment()
    environ.add_name('work', Namespace())
    for task in tasks:
        environ.execute(task.__class__.__name__, task)

if __name__ == '__main__':
    main()

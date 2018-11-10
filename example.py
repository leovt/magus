from task import Import, Select, Print
from backend import Environment, Namespace

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

import argparse, os, time

from pwn import *

parser = argparse.ArgumentParser(description='Borrador de metadados para varias extensiones.')
parser.add_argument('name', action='store', type=str, help='Nombre del fichero.')

args = parser.parse_args()


def extractor():

    p1 = log.progress('Extrayendo los metadatos')
    p1.status('Iniciando')

    time.sleep(2)

    print(f'Tu archivo tiene la siguiente información:\n')

    au = os.system("exiftool " + args.name + " | grep -i author")
    print(au)
    cr = os.system("exiftool " + args.name + " | grep -i creator")
    print(cr)
    pr = os.system("exiftool " + args.name + " | grep -i producer")
    print(pr)
    cd = os.system("exiftool " + args.name + " | grep -i 'create date'")
    print(cd)
    md = os.system("exiftool " + args.name +  "| grep -i 'modify date'")
    print(md)
    p1.success("Listo")

    q1 = input("¿Deseas borrar todos los metadatos de tu archivo? [S/n]\n" "Introduce 'e' para salir.\n")
    
    if q1 == ("s") or q1 == ("S"):
        os.system("exiftool -all= " + args.name)
        print("No toda la información se puede borrar. La que permanece en tu archivo es la siguiente:\n")
        os.system("exiftool " + args.name)
    elif q1 == ("n") or q1 == ("N"):
        print("No sé lo que quieres entonces.\nEmpecemos de nuevo.")
        extractor()
    elif q1 == ("d") or q1 == ("D"):
        print("Opción paranoica.")
    elif q1 == ("e") or q1 == ("E"):
        return 0
    else:
        print("Opción inválida. Te daré una oportunidad más.\n")
        extractor()

    print("\nAhora tienes dos archivos, el original '{}_original' y el nuevo '{}'.".format(args.name, args.name))

    return 0


def main():
    extractor()


if __name__ == '__main__':
    main()


import datetime
import os
import subprocess
from funciones import older_than


PATH = '/home/observatorio/Dropbox/back/'
FECHA = datetime.datetime.now().strftime('%d-%b-%Y_%H:%M')
PATH_SEMANAL = '/media/observatorio/backup_semanal'


PFA_DGC = '{}backup_pfa_dgc_{}.tar'.format(PATH, FECHA)
PFA_DGC95 = '{}backup_postgres95_pfa_dgc_{}.backup'.format(PATH, FECHA)
FEU = '{}backup_feu_{}.tar'.format(PATH, FECHA)

subprocess.call(['/usr/lib/postgresql/9.5/bin/pg_dump',
	         '--format=c', '--port=5433',
                 '--dbname=pfa_dgc', '--file=' + PFA_DGC95])
subprocess.call(['pg_dump', '--format=t',
                 '--dbname=pfa_dgc', '--file=' + PFA_DGC])
subprocess.call(['pg_dump', '--format=t',
                 '--dbname=feu', '--file=' + FEU])

#delete files older than 15 days
for file in older_than(PATH, 15):
    os.remove(wp)

#copy backup files & homedir to external drive
subprocess.call(['cp', '-r', '~', '/media/observatorio/OSV_Backup'])

#on mondays, also copy to the weekly folder
if datetime.datetime.now().weekday() == 0 or older_than(PATH_SEMANAL, 7):
    subprocess.call(['cp', PFA_DGC95, PATH_SEMANAL])
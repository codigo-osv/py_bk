import datetime
import os
import subprocess
import classes

FECHA = datetime.datetime.now().strftime('%d-%b-%Y_%H:%M')
PATH = '/home/observatorio/Dropbox/back/'
PATH_HOME = '/home/observatorio'
PATH_DIARIO = '/media/observatorio/OSV_Backup'
PATH_SEMANAL = '/media/observatorio/backup_semanal'

PFA_DGC95 = '{}backup_postgres95_pfa_dgc_{}.backup'.format(PATH, FECHA)
FEU = '{}backup_feu_{}.tar'.format(PATH, FECHA)

subprocess.call(['/usr/lib/postgresql/9.5/bin/pg_dump',
                 '--format=c', '--port=5433',
                 '--dbname=pfa_dgc', '--file=' + PFA_DGC95])
subprocess.call(['pg_dump', '--format=t',
                '--dbname=feu', '--file=' + FEU])

# delete files older than 15 days
td = classes.TimedDirectory(PATH)
for file in td.oldest_files_list(15):
    os.remove(file)

# copy backup files & homedir to external drive
subprocess.call(['rsync', '-av', PATH_HOME, PATH_DIARIO])

# on mondays or after 1 week, also copy to the weekly folder
td.path = PATH_SEMANAL
if datetime.datetime.now().weekday() == 0 or td.newest_file_older_than(7):
    subprocess.call(['cp', PFA_DGC95, PATH_SEMANAL])

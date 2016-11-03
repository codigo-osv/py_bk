import datetime
import os
import subprocess


PATH = '/home/observatorio/Dropbox/back/'
FECHA = datetime.datetime.now().strftime('%d-%b-%Y_%H:%M')


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
flist = os.listdir(PATH)
rng = datetime.datetime.now() - datetime.timedelta(days=15)
for file in flist:
    wp = PATH + file
    lmod = os.stat(wp).st_mtime
    dlmod = datetime.datetime.fromtimestamp(lmod)
    if dlmod < rng:
       os.remove(wp)

#copy backup files to external drive
subprocess.call(['cp', '-r', PATH, '/media/observatorio/OSV_Backup'])
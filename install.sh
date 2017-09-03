#!/bin/bash

if [ "$(whoami)" != 'root' ]; then
	echo "You have no permission to run $0 as non-root user."
	exit 1;
fi

echo "#!/bin/bash" > "fetchAll.sh"
echo "python3.5 $(pwd)/fetchPackages.py cran -1 $(pwd)" >> "fetchAll.sh"
echo "python3.5 $(pwd)/fetchPackages.py rubygems -1 $(pwd)" >> "fetchAll.sh"
echo "python3.5 $(pwd)/fetchPackages.py npm -1 $(pwd)" >> "fetchAll.sh"
echo "python3.5 $(pwd)/fetchDependencies.py cran -1 $(pwd)" >> "fetchAll.sh"
echo "python3.5 $(pwd)/fetchDependencies.py rubygems -1 $(pwd)" >> "fetchAll.sh"
echo "python3.5 $(pwd)/fetchDependencies.py npm -1 $(pwd)" >> "fetchAll.sh"

echo "$(date -d "+5 minutes" +"%M %H %d %m") * $(pwd)/fetchAll.sh >> $(pwd)/log.log 2>&1" > "schedule.cron"
crontab "schedule.cron"
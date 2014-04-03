#!/bin/sh
# by j00zek 2014
#Pobieranie przykladowych pikon dla PiconSelektora
Akcja="$1"
Katalog="$2"
NaszURL="$3"

TranslatedEcho() {
if [ -f /jzk/bin/translate ]; then
  echo `/jzk/bin/translate "$1"`
else
  echo "$1"
fi 
}

case $Akcja in
	SYNC) #czyszczenie pikon na wypadek zmian na web
		rm -rf /tmp/.PICONS.SYNCED
		rm -rf $Katalog/$pikon.png
		#czy mamy internet?
		ping -c 1 www.wp.pl
		[ $? -gt 0 ] && exit 0
		#tworzenie listy picon
		pikonyOnline=`wget $NaszURL -O - 2>/dev/null | grep "\.png" | sed "s/^.*href=\"//" | sed "s/\.png\">.*$//"`
		#pobieranie nie pobranych wczesniej pikon
		for pikon in $pikonyOnline
		do
		if [ ! -f $Katalog/$pikon.png ]; then
			echo "Downloading $pikon ..."
			wget $NaszURL$pikon.png -O $Katalog/$pikon.png 2>/dev/null
		fi
		touch /tmp/.PICONS.SYNCED
		done
    ;;
	PICONS) # pobieranie i instalacja archiwum
		cd $Katalog
		TranslatedEcho 'Downloading picons...'
		wget $NaszURL -O $Katalog/picons.tar.gz 2>/dev/null 
		if [ -f $Katalog/picons.tar.gz ]; then
			TranslatedEcho 'Unpacking picons...'
			tar -xzf $Katalog/picons.tar.gz
			TranslatedEcho 'Picons installed properly'
            rm -f $Katalog/picons.tar.gz
			if [ -f /jzk/bin/UpdatePicons.sh ]; then
				TranslatedEcho 'Syncing picons with lamedb...'
				/jzk/bin/UpdatePicons.sh
			fi
			  
		else
            TranslatedEcho 'Error installing picons :('
		fi 
	;;
esac


exit 0
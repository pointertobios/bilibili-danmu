.PHONY: install uninstall

install:
	cp bilibili-danmu.py /usr/bin/
	chmod +x /usr/bin/bilibili-danmu.py
	cp bilibili-danmu.desktop /usr/share/applications/

uninstall:
	rm /usr/bin/bilibili-danmu.py
	rm /usr/share/applications/bilibili-danmu.desktop

.PHONY: install uninstall

install:
	cp bilibili-danmu.py /usr/bin/
	chmod +x /usr/bin/bilibili-danmu.py
	cp bilidanmu.service /etc/systemd/system/

uninstall:
	rm /usr/bin/bilibili-danmu.py
	rm /etc/systemd/system/bilidanmu.service

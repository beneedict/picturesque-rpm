srpm:
	dnf -y install rpmdevtools curl
	spectool -g -R picturesque.spec
	rpmbuild -bs --define "_sourcedir $(shell pwd)" --define "_srcrpmdir $(outdir)" picturesque.spec

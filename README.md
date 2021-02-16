# semrep_hype

Explore linguistic semantic primes on the [Europarl corpus](https://www.statmt.org/europarl/index.html).

### Usage

* Run a local [MariaDB](https://mariadb.org/) database that has a `root` user on the default port or change the connection settings in `funny_script.py`.
* Get the `mariadb` package via `pip3 install mariadb`.
* Run `./download.sh` to download the Europarl corpus and extract all sentences that contain semantic primes.


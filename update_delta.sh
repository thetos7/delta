sed -i -e '1,/^$/b' -e '/if __name/,$b' -e 's/^/    /' delta.py
sed -i -e '/^    app =/i def init():' delta.py

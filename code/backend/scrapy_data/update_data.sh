list="110000 420100 310000 110000 420100 310000"
for id in $list
do
sed -i "s/CITY_ID = 0/CITY_ID = $id/g" ./scrapy_data/settings.py
scrapy crawl bk_houselist -s CITY_ID="$id" --nolog
scrapy crawl bk_bublelist -s CITY_ID="$id" --nolog
sed -i "s/CITY_ID = $id/CITY_ID = 0/g" ./scrapy_data/settings.py
done
echo "update succeed!"
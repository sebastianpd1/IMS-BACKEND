response = [
    {
	"products_id":1,
	"quantity": -10,
	"sales_id":None,
	"purchases_id": None,
	"warehouses_id":1
},
{
	"products_id":1,
	"quantity": -10,
	"sales_id":None,
	"purchases_id": None,
	"warehouses_id":1
},
{
	"products_id":1,
	"quantity": -10,
	"sales_id":None,
	"purchases_id": None,
	"warehouses_id":1
},

]
purchases_id = 10
for e in response:
    e["purchases_id"]=purchases_id

print(response)
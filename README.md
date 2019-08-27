# EndPoints:

```md
	•	/transactions/new/map
	•	/purchases/all
	•	/products/all
	•	/sales/all
  
```

## INVENTORY `PRODUCTS` TABLE:

### TO `ADD` A NEW RECORD FOR "PRODUCTS" 	•	/products/all

```md	
	Method: POST
	/products/all
```
- Body must contain the following:

```md	
	 {
  	 "item":"chocolate",
	 "description":"food",
	 "quantity":"7"
         }
```
- First: Item Name and description
- Second: you must put an initial quantity

### TO `GET ALL` RECORDS OF "PRODUCTS"

```md	
	Method: GET
	/products/all
```
- Retrieves all records (products) and the related `Transactions` of each item


## INVENTORY `PURCHASES` TABLE •	/purchases/all

### TO `ADD` A NEW RECORD FOR "PURCHASES"

```md	
	Method: POST
	/purchases/all
```
- Adds a record with `id` and `Creation Date`


### TO `GET ALL` RECORDS OF "PURCHASES"

```md	
	Method: GET
	/purchases/all
```
- Retrieves all records on this table, including the related products


## INVENTORY `SALES` TABLE: 	•	/sales/all

### TO `ADD` A NEW RECORD FOR "SALES"

```md	
	Method: POST
	/sales/all
```
- Adds a record with `id` and `Creation Date`


### TO `GET ALL` RECORDS OF "SALES"

```md	
	Method: GET
	/sales/all
```
- Retrieves all records on this table, including the related product


## INVENTORY `TRANSACTIONS` TABLE:

### TO `ADD` A NEW RECORD FOR "TRANSACTIONS" (CAN BE IN OR OUT)

```md	
	Method: POST
	/transactions/new
```
- Body must contain the following:
(AT LEAST ONE OR MORE OBJECTS)

```md	
	{
	"products_id":3,
	"quantity":5,
	"purchases_id": null
	},
  {
	"products_id":4,
	"quantity":5,
	"purchases_id": null
	}
```
- First you should have a product with an initial quantity
- Second: if it's a sale you must not include the `sales_id`, because it will be created automatically, and viceversa with `purchases`
- third: you must set a `warehouse_id`, that's mandatory, consider the following:
1.MAIN
2.MOTORCYCLE1
3.MOTORCYCLE2
4.MOTORCYCLE3 

- If its a `PURCHASE` you should set the quantity amount to positive, if its `SALE` you should set it to negative (example : -3)

### TO `GET ALL` RECORDS OF "TRANSACTIONS" •	/transactions/new/map

```md	
	Method: GET
	/transactions/new/map
```
- Retrieves all records on this table




After we have `use` a database, there's a special variable available. 
The variable is called `db`

# Finding documents

Show all documents in a collection (but only the first ten)
```
db.listingsAndReviews.find().limit(10)
```

Prettify the output with the `.pretty()` function

```
db.listingsAndReviews.find().pretty().limit(10)
```

```
db.listingsAndReviews.find({
    'beds':3
}).pretty().limit(10)
```

With projections
```
db.listingsAndReviews.find({
    'beds':3
},{
    'name':1,
    'beds':1
}).pretty().limit(10)
```

## with more than one critera
```
db.listingsAndReviews.find({
    'beds':3,
    'bedrooms':3
},{
    'name':1,
    'beds':1,
    'bedrooms':1
}).prettty.limit(10)
```
## get number of results

```
db.listingsAndReviews.find({
    'beds':3,
    'bedrooms':3
},{
    'name':1,
    'beds':1,
    'bedrooms':1
}).count()
```

## comparison
```
db.listingsAndReviews.find({
    'beds': {
        '$gt':4
    }
}, {
    'name':1,
    'beds':1
})
```

## greater than equal
```
db.listingsAndReviews.find({
    'beds': {
        '$gte':4
    }
}, {
    'name':1,
    'beds':1
})
```

## find by range
```
db.listingsAndReviews.find({
    'beds': {
        '$gte':4,
        '$lte':8
    }
}, {
    'name':1,
    'beds':1
})
```
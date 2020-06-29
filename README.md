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

### Find all listings with 3 beds and only show the listing name and the number of beds
```
db.listingsAndReviews.find({
    'beds': 3
}, {
    'name':1,
    'beds':1
})
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

## Find in a field that is an array

### eg. find all listings that have 'Hot Tub'
```
db.listingsAndReviews.find({
    'amenities':'Cable TV'
}, {
    name: 1,
    amenities: 1
}).pretty()
```

### eg. find all listings that have Wifi and Laptop friendly workspace
```
db.listingsAndReviews.find({
    'amenities': {
        '$all':['Wifi', 'Laptop friendly workspace']
    }
}, {
    'name':1,
    'amenities':1
}).pretty()
```

## EG. find all listings that have doorman OR 'Host greets you'
```
db.listingsAndReviews.find({
    'amenities': {
        '$in':['Doorman', 'Host greets you']
    }
}, {
    name:1,
    amenities:1
}).pretty()
```

## Find all listings in Canada
```
db.listingsAndReviews.find({
    'address.country':'Singapore'
}, {
    'name':1,
    'address.country':1
})
```

# Find all listings that are in Canada or in Brazil
```
db.listingsAndReviews.find({
    'address.country': {
        '$in':['Canada', 'Brazil']
    }
}, {
    'name':1,
    'address.country':1
})
```

# Find by one of this critera: 
# either listing is from Canada and have >= 5 bed rooms
# OR listing is from Brazil

```
db.listingsAndReviews.find({
    '$or':[
        {
            'address.country': "Canada",
            'bedrooms' : {
                '$gte': 3
            }
        },
        {
            'address.country':'Brazil'
        }
    ]
}, {
    'name': 1,
    'bedrooms': 1,
    'address.country': 1
}).limit(100)
```

# Display all listings that have the world "Spacious" within its name anywhere
```
db.listingsAndReviews.find({
    'name': {
        "$regex":"Spacious", "$options":'i'
    }
}, {
    'name':1
})
```

# Display all listings that have the word "spacious" in it, and are in Canada
```
db.listingsAndReviews.find({
    'name': {
        "$regex":"Spacious", "$options":'i'
    },
    'address.country':'Canada'
}, {
    'name':1,
    'address.country':1
})
```
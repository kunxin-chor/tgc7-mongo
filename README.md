# Installing the dependencies

```
pip3 install -r requirements.txt
```

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

## Find all listings in Singapore
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
# Find all documents that has a particular id in one of its array elements
```
db.animals.find({
    'checkups._id':ObjectId('5f0324fe22390f7fefb455aa')
}).pretty()

```
# Find all documents that has a particular id in one of its array elements
# and only return that array
```
db.animals.find({
    'checkups._id':ObjectId('5f0324fe22390f7fefb455aa')
},{
    'checkups':1
})
```

# Find all documents that has a particular id in one of its array elements
# and return only the element that matches that particular id
```
db.animals.find({
    'checkups._id':ObjectId('5f0324fe22390f7fefb455aa')
}, {
    'checkups': {
        '$elemMatch': {
            '_id':ObjectId('5f0324fe22390f7fefb455aa')
        }
    }
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

# MOVIES DB

## Find all movies not produced in the USA
```
db.movies.find({
	'countries': {
		'$nin': ['USA']
	}
}, {
	'title':1,
	'countries':1
})
```

Alternative answer:
```
db.movies.find({
	'countries': {
		'$not' : {
			'$in':['USA']
		}
	}
}, {
	'title':1,
	'countries':1
})
```

## Find movies that have at least 3 wins in the awards object
```
db.movies.find({
    'awards.nominations':{
        '$gte':3
    }
}, {
    title: 1
}).pretty()
```

## Find movies that has at least 3 nominations
```
db.movies.find({'awards.nominations': { '$gte': 3 }},{'title':1, 'awards.nominations':1}).pretty()
```

## Find movies that cast Tom Cruise
```
db.movies.find({'cast': 'Tom Cruise'}, {'title':1, 'cast':1})
```

## Find movies that includes Charlie Chaplin in the directors
```
db.movies.find({
    'directors': 'Charles Chaplin'
},{
    'title':1,
    'directors': 1
})
```

# Creating a new database in Mongo

The code below will create a new database named `animal_shelter`
```
use animal_shelter
```

## Create a new collection
Insert a new document into the non-existent collection and Mongo will create it

```
db.animals.insert({
    "name":"Cookie",
    "breed":"Golden Retriever",
    "animal_type":"Dog"
})
```

```
db.animals.insert({
    "name":"Potato",
    "breed":"Shiba Inu",
    "animal_type":"Dog",
    "checkups": [
        {
            "vet":"Dr. Chua",
            "diagnosis":"Hips problem",
            "date":"1/12/2019"
        },
        {
            "vet":"Dr Chua",
            "diagnosis":"Skin irration",
            "date":"25/06/2019"
        }
        
    ]
})
```

## Insert many vets at one go
```
db.vets.insertMany([
    {
        "name":"Dr Chua",
        "license":"X123456",
        "clinic":"Sunshine Way Pet Clinic",
        "address": {
            "street":"Sunshine Way Ave 1",
            "blk":"123",
            "unit":"#01-06"
        }
    },
    {
        "name":"Dr Leon Lai",
        "license":"A123456D",
        "clinic":"Serene Center Pet Care",
        "address": {
            "street":"Bukit Timah Drive 1",
            "blk":"220",
            "unit":"01-23"
        }
    }
])
```

## Change the vet `Dr Chua` to `Dr Clarence Chua`
```
db.vets.update({
    '_id':ObjectId("5ef9e7665c19070d2777cbfc")
},{
    "$set": {
        "name":"Dr. Clarence Chua"
    }
})
```

## Add a new checkup to an animal
```
db.animals.updateOne({
    "_id":ObjectId("5efc8a26f9f4582616f7940e")
}, {
    "$push": {
        'checkups': {
            "vet":"Dr Chua",
            "date": new Date("2020-06-29"),
            "diagnosis":"Fluffy has diabetes. Must workout more"
        }
    }
})
```

# UploadCare

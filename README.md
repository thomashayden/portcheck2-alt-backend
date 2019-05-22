# portcheck2-alt-backend
An alternate portcheck 2 backend using json and no annoying things like graphql

# Spec
## Example Data Structure

    { "Building" : [
        { "Name" : "WIL",
          "Room" : [
            { "Number" : "103" },
            { "Number" : "104" },
            { "Number" : "105" }
          ]
        },
        { "Name" : "PAN",
          "Room" : [
            { "Number" : "733" },
            { "Number" : "831" },
            { "Number" : "1006" }
          ]
        },
        { "Name" : "337",
          "Room" : [
            { "Number" : "301" },
            { "Number" : "309" },
            { "Number" : "108" }
          ]
        }
      ]
    }

## Schema

### Rules:
- Keys cannot start with a '~' (reserved for system information) or a '*' (reserved for specifying
command type)
- All keys must be strings

### Examples:
    { "Building" : [
        { "Name",
          "Rooms" : [
            { "Number" }
          ]
        }
      ]
    }

## Different Servers (different schemas like Portcheck and Printers)
This will be dealt with later as it is a relatively easy detail to sort out. It may be a key at the
beginning which specifies the server being used or a different endpoint. Either way the rest of
this is the same.schema 

## Querying

### Notes:
- Keys starting with a '~' are system information (currently only array lengths)
- Accessing elements in an array is done either by the index (with `"*[n]"`) where n is a number, ~~or
with a key value pair (`["Number" : "733"]`)~~ (may be implemented later if needed)

### Examples:
    { "*query" : { "Building" : { "*[1]" : { "Name" : {} } } } }
    ==> "PAN"
    { "*query" : { "Building" : { "*[1]" : { "Room" : {} } } } }
    ==> { "~arr" : { "~len" : 3 }
    { "*query" : { "Building" : { "*[2]" : { "Room" : { "*[0]" : { "Number" : {} } } } } } }
    ==> 301
    { "*query" : { "Building" : {} } }
    ==> { "~arr" : { "~len" : 3 } }
    { "*query" : { "Building" : { "*[1]" : {} } } }
    ==> { "Name" : "PAN",
          "Room" : { "~arr" : { "~len" : 3 } }
        }

## Mutation

### Changing a value at the end of a path

    { "*chg" : { "Building" : { "*[1]" : { "Name" : "YMC" } } } }
    ==> "YMC"
    { "*chg" : { "Building" : { "*[1]" : { "Room" : { "*[0]" : { "Number" : 302 } } } } } }
    ==> 302

### Deleting
Can only delete elements from an array. A query wrapped in `{ "*del" : <query> }`

    { "*del" : { "Building" : { "*[1]" : {} } } }
    ==> { "*del" : { "Building" : { "*[1]" : {} } } }
    { "*del" : { "Building" : { "*[0]" : { "Room" : { "*[2]" : {} } } } } }
    ==> { "*del" : { "Building" : { "*[1]" : {} } } }

### Adding
Can only add elements to an array.

    { "*add" : { "Building" : { "*[]" : { "Name" : "PAN",
                                          "Room" : [
                                            { "Number" : "733" },
                                            { "Number" : "831" },
                                            { "Number" : "1006" }
                                          ]
                                        } } }
    ==> { "*add" : { "Building" : { "*[]" : { "Name" : "PAN",
                                               "Room" : [
                                                 { "Number" : "733" },
                                                 { "Number" : "831" },
                                                 { "Number" : "1006" }
                                               ]
                                             } } }
    { "*add" : {"Building" : { "*[0]" : { "Room" : { [] : { "Number" : 109 } } } } } }
    ==> { "*add" : {"Building" : { "*[0]" : { "Room" : { [] : { "Number" : 109 } } } } } }

## Errors
If a command is issued incorrectly, a response will be returned with the following format

    { "~err" : { "~msg" : <error message> } }
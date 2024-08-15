# MemSan

## Compile

```
cmake . && make
```

## Run AST dump to MemSan.dump

``` 
./LOG6302 <file_to_analyze>
```

## Run analyses

```
python3 src/Analyzer.py
```  

Will output all .dot files in src

## Metrics extraction

```
python3 src/Analyzer.py -tp1
```

Will output in src/metrics.txt

## UML

 Same but in the tp2 directory
 Will output .dot file in src/

# Error 11000:
#### PS C:\Users\ricki\OneDrive\Documentos\TiendaIA-Equipo5> docker compose exec mongo mongosh tienda --quiet --eval "db.productos.insertOne({id: 1, nombre: 'duplicado'})"
#### MongoServerError: E11000 duplicate key error collection: tienda.productos index: id_1 dup key: { id: 1 }

#### What's next Debug this Compose error with Gordon → docker ai "help me fix this compose error"

##### PS C:\Users\ricki\OneDrive\Documentos\TiendaIA-Equipo5> docker compose exec mongo mongosh tienda --quiet --eval "db.productos.find({id: 3}).explain('executionStats').executionStats"        
{
  executionSuccess: true,
  nReturned: 0,
  executionTimeMillis: 5,
  totalKeysExamined: 0,
  totalDocsExamined: 0,
  executionStages: {
    stage: 'FETCH',
    nReturned: 0,
    executionTimeMillisEstimate: 0,
    works: 1,
    advanced: 0,
    needTime: 0,
    needYield: 0,
    saveState: 0,
    restoreState: 0,
    isEOF: 1,
    docsExamined: 0,
    alreadyHasObj: 0,
    inputStage: {
      stage: 'IXSCAN',
      nReturned: 0,
      executionTimeMillisEstimate: 0,
      works: 1,
      advanced: 0,
      needTime: 0,
      needYield: 0,
      saveState: 0,
      restoreState: 0,
      isEOF: 1,
      keyPattern: { id: 1 },
      indexName: 'id_1',
      isMultiKey: false,
      multiKeyPaths: { id: [] },
      isUnique: true,
      isSparse: false,
      isPartial: false,
      indexVersion: 2,
      direction: 'forward',
      indexBounds: { id: [ '[3, 3]' ] },
      keysExamined: 0,
      seeks: 1,
      dupsTested: 0,
      dupsDropped: 0
    }
  }
}


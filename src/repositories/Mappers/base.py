

class DataMapper:
    db_model = None
    schema = None

    def map_to_domain_entity(self, db_model):
        return self.schema.model_validate(db_model, from_attributes=True)

    def map_to_persistent_entity(self, schema):
        return self.db_model(**schema, from_attributes=True)
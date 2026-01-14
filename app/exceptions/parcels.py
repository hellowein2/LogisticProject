class ParcelNotFoundError(Exception):
    pass

class ParcelAlreadyExistsError(Exception):
    pass


class InvalidParcelTypeError(Exception):
    def __init__(self, parcel_type_id: int):
        super().__init__(f"Invalid parcel_type_id={parcel_type_id}")
        self.parcel_type_id = parcel_type_id

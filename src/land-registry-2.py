from pyteal import *

def land_registry():

    # Define the schema of the global state
    global_schema = GlobalSchema(
        num_uints=1,
        num_byte_slices=2
    )

    # Define the schema of the local state
    local_schema = LocalSchema(
        num_uints=0,
        num_byte_slices=0
    )

    # On app initialization
    def on_initialization():
        return Seq([
            App.globalPut(Bytes("owner"), Txn.sender()),
            App.globalPut(Bytes("land"), Bytes("")),
            App.globalPut(Bytes("landID"), Int(0)),
            Return(Int(1))
        ])

    # On every call after initialization
    def on_update_call():
        is_owner = App.globalGet(Bytes("owner")) == Txn.sender()

        # Owner can update land info or transfer ownership
        handle_owner_call = Cond(
            [Txn.application_args[0] == Bytes("update_land"), 
             Seq([App.globalPut(Bytes("land"), Txn.application_args[1]),
                  App.globalPut(Bytes("landID"), Txn.application_args[2]),
                  Return(Int(1))])],

            [Txn.application_args[0] == Bytes("transfer_ownership"), 
             Seq([App.globalPut(Bytes("owner"), Txn.application_args[1]),
                  Return(Int(1))])]
        )

        # If not owner, then reject the transaction
        handle_not_owner_call = Seq([
            Assert(Not(is_owner)),
            Return(Int(0))
        ])

        return Cond(
            [is_owner, handle_owner_call],
            [Not(is_owner), handle_not_owner_call]
        )

    # Combine initialization and update calls
    program = Cond(
        [Txn.application_id() == Int(0), on_initialization()],
        [Txn.application_id() != Int(0), on_update_call()]
    )

    return compileTeal(program, mode=Mode.Application, version=4)


if __name__ == "__main__":
    print(compileTeal(land_registry(), mode=Mode.Application, version=4))

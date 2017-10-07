module Update exposing (..)

import Msgs exposing (Msg(..))
import Models exposing (Model)

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Msgs.OnFetchEntries response ->
            ( { model | entries = response }, Cmd.none )

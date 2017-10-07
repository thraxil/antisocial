module Update exposing (..)

import Msgs exposing (Msg(..))
import Models exposing (Model)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Msgs.OnFetchEntries response ->
            ( { model | entries = response }, Cmd.none )

        KeyMsg code ->
                case code of
                    74 -> -- j
                         ( nextEntry model, Cmd.none )

                    75 -> -- k
                         ( prevEntry model, Cmd.none )

                    82 -> -- r
                         ( model, Cmd.none )
                             
                    _ -> -- don't care
                        ( model, Cmd.none )


nextEntry : Model -> Model
nextEntry model =
    { model | drop = model.drop + 1 }

prevEntry : Model -> Model
prevEntry model =
    { model | drop = max 0 model.drop - 1 }

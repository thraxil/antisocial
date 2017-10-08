module Update exposing (..)

import Commands exposing (updateEntryCmd, fetchEntries)
import Msgs exposing (Msg(..))
import Models exposing (Model, Fetched)
import RemoteData exposing (WebData)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Msgs.OnFetchEntries response ->
            ( modelFromResponse model response, Cmd.none )

        KeyMsg code ->
                case code of
                    74 -> -- j
                         ( nextEntry model, updateEntryCmd model )

                    75 -> -- k
                         ( prevEntry model, Cmd.none )

                    82 -> -- r
                         ( model, fetchEntries )
                             
                    _ -> -- don't care
                        ( model, Cmd.none )

        Msgs.OnEntrySave _ ->
            ( model, Cmd.none )


modelFromResponse : Model -> WebData (Fetched) -> Model
modelFromResponse model response =
    let
        unread =
            case response of
                RemoteData.Success data ->
                    Maybe.withDefault [] (List.tail data.entries)

                _ ->
                    []
                        
    in                
        { model | fetched = response
        , read = []
        , current = Nothing
        , unread = unread
        }


nextEntry : Model -> Model
nextEntry model =
    let
        read =
            case model.current of
                Just current ->
                    model.read ++ (current :: [])

                Nothing ->
                    []

        unread =
            case List.tail model.unread of
                Just entries ->
                    entries

                Nothing ->
                    []
                        
    in
        { model | read = read
        , current = List.head model.unread
        , unread = unread
        }


prevEntry : Model -> Model
prevEntry model =
    let
        unread =
            case model.current of
                Just current ->
                    current :: model.unread

                Nothing ->
                    model.unread

        read =
            case List.tail (List.reverse model.read) of
                Just entries ->
                    List.reverse entries

                Nothing ->
                    []
    in
        { model | read = read
        , current = List.head (List.reverse model.read)
        , unread = unread
        }

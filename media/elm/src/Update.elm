module Update exposing (..)

import Commands exposing (updateEntryCmd, fetchEntries)
import Msgs exposing (Msg(..))
import Models exposing (Model, Fetched, Entry)
import RemoteData exposing (WebData)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Msgs.OnFetchEntries response ->
            ( modelFromResponse model response, Cmd.none )

        KeyMsg code ->
                case code of
                    74 -> -- j (next)
                         ( nextEntry model, updateEntryCmd model )

                    75 -> -- k (prev)
                         ( prevEntry model, Cmd.none )

                    82 -> -- r (refresh the list of entries)
                         ( model, fetchEntries )
                             
                    _ -> -- don't care
                        ( model, Cmd.none )

        Msgs.OnEntrySave (Ok er ) ->
            ( { model | unreadCnt = Just er.unread }, Cmd.none )

        Msgs.OnEntrySave (Err error) ->
            ( model, Cmd.none )


modelFromResponse : Model -> WebData (Fetched) -> Model
modelFromResponse model response =
    let
        unread =
            entriesOrEmpty response
    in
        { model | read = []
        , current = Nothing
        , unread = unread
        , unreadCnt = Just (List.length unread)
        }


entriesOrEmpty : WebData (Fetched) -> List Entry
entriesOrEmpty response =
    case response of
        RemoteData.Success data ->
            data.entries

        _ ->
            []


nextEntry : Model -> Model
nextEntry model =
    { model | read = maybeCons model.current model.read
    , current = List.head model.unread
    , unread = Maybe.withDefault [] (List.tail model.unread)
    }


prevEntry : Model -> Model
prevEntry model =
    { model | read = Maybe.withDefault [] (List.tail model.read)
    , current = List.head model.read
    , unread = maybeCons model.current model.unread
    }


maybeCons : Maybe a -> List a -> List a
maybeCons maybeA listA =
    case maybeA of
        Just thing ->
            thing :: listA

        Nothing ->
            listA

module Commands exposing (..)

import Http
import Json.Decode as Decode
import Json.Decode.Pipeline exposing (decode, required, optional, hardcoded)
import Json.Encode as Encode
import Msgs exposing (Msg)
import Models exposing (EntryId, Entry, Fetched, EntryUpdate, Model)
import RemoteData


-- main fetch of all unread entries

fetchEntries : Cmd Msg
fetchEntries =
    Http.get fetchEntriesUrl entriesDecoder
        |> RemoteData.sendRequest
        |> Cmd.map Msgs.OnFetchEntries


fetchEntriesUrl : String
fetchEntriesUrl =
    "/api/entries/"


entriesDecoder : Decode.Decoder (Fetched)
entriesDecoder =
    decode Fetched
        |> required "unread" Decode.int
        |> required "entries" (Decode.list entryDecoder)


entryDecoder : Decode.Decoder Entry
entryDecoder =
    decode Entry
        |> required "id" Decode.int
        |> required "title" Decode.string
        |> required "link" Decode.string
        |> optional "description" Decode.string ""
        |> required "published" Decode.string
        |> required "feed_title" Decode.string


-- mark an entry as read, then update the unread count


updateUrl : EntryId -> String
updateUrl id =
    "/api/entry/" ++ toString(id) ++ "/"


updateEntryCmd : Model -> Cmd Msg
updateEntryCmd model =
    let
        nextCurrent = List.head model.unread
    in
        case nextCurrent of
            Just entry ->
                updateEntryRequest entry
                    |> Http.send Msgs.OnEntrySave

            Nothing ->
                Cmd.none


updateEntryRequest : Entry -> Http.Request EntryUpdate
updateEntryRequest entry =
    Http.request
        { body = Encode.object [ ( "read", Encode.bool True )] |> Http.jsonBody
        , expect = Http.expectJson entryUpdateDecoder
        , method = "PUT"
        , timeout = Nothing
        , url = updateUrl entry.id
        , withCredentials = True
        , headers = []
        }
        
           
entryUpdateDecoder : Decode.Decoder EntryUpdate
entryUpdateDecoder =
    decode EntryUpdate
        |> required "unread_count" Decode.int

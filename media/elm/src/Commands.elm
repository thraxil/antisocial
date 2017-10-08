module Commands exposing (..)

import Http
import Json.Decode as Decode
import Json.Decode.Pipeline exposing (decode, required, optional, hardcoded)
import Msgs exposing (Msg)
import Models exposing (EntryId, Entry, Fetched)
import RemoteData

fetchEntries : Cmd Msg
fetchEntries =
    Http.get fetchEntriesUrl entriesDecoder
        |> RemoteData.sendRequest
        |> Cmd.map Msgs.OnFetchEntries

fetchEntriesUrl : String
fetchEntriesUrl =
    "/api/elmentries/"

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
        |> optional "read" Decode.bool False

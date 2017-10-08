module Msgs exposing (..)

import Http
import Keyboard
import Models exposing (Fetched, EntryUpdate)
import RemoteData exposing (WebData)

type Msg
    = OnFetchEntries (WebData (Fetched))
    | KeyMsg Keyboard.KeyCode
    | OnEntrySave (Result Http.Error EntryUpdate)

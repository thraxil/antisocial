module Msgs exposing (..)

import Keyboard
import Models exposing (Fetched)
import RemoteData exposing (WebData)

type Msg
    = OnFetchEntries (WebData (Fetched))
    | KeyMsg Keyboard.KeyCode

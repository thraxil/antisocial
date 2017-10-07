module Msgs exposing (..)

import Keyboard
import Models exposing (Entry)
import RemoteData exposing (WebData)

type Msg
    = OnFetchEntries (WebData (List Entry))
    | KeyMsg Keyboard.KeyCode

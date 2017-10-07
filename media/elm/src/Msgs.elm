module Msgs exposing (..)

import Models exposing (Entry)
import RemoteData exposing (WebData)

type Msg
    = OnFetchEntries (WebData (List Entry))

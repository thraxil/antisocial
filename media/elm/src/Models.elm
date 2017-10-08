module Models exposing (..)

import RemoteData exposing (WebData)

type alias Fetched =
    { unread : Int
    , entries : List Entry
    }

type alias Model =
    { fetched : WebData (Fetched)
    , read : List Entry
    , current : Maybe Entry
    , unread : List Entry
    , unreadCnt : Maybe Int
    }

initialModel : Model
initialModel =
    { fetched = RemoteData.Loading
    , read = []
    , current = Nothing
    , unread = []
    , unreadCnt = Nothing
    }

type alias EntryId = Int


type alias Entry =
    { id : EntryId
    , title : String
    , link : String
    , description : String
    , published : String
    , feed_title : String
    , read : Bool
    }

type alias EntryUpdate =
    { unread : Int }

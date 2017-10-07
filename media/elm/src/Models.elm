module Models exposing (..)

import RemoteData exposing (WebData)

type alias Model =
    { unread : Int
    , entries : WebData (List Entry)
    , current : Maybe Int
    }

initialModel : Model
initialModel =
    { unread = 0
    , entries = RemoteData.Loading
    , current = Nothing
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
    , current : Bool
    }

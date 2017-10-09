module View exposing (..)

import Entries.List
import Html exposing (Html, div, text)
import Html.Attributes exposing (class)
import Models exposing (Model, Entry, Fetched)
import Msgs exposing (Msg)
import RemoteData exposing (WebData)


view : Model -> Html Msg
view model =
    div []
        [ Entries.List.currentRow model.current
        , Entries.List.view model.unread              
        , unreadCounter model.unreadCnt
        ]


unreadCounter : Maybe Int -> Html Msg
unreadCounter maybeCnt =
    case maybeCnt of
        Just unreadCnt ->
            div [ class "unread-counter" ]
                [ text (toString(unreadCnt) ++ " unread") ]

        Nothing ->
            text "no count yet"


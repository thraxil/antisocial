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
        [ page model
        , unreadCounter model.fetched
        ]


page : Model -> Html Msg
page model =
    div []
        [ Entries.List.currentRow model.current
        , Entries.List.view model.unread
        ]
                

unreadCounter : WebData (Fetched) -> Html Msg
unreadCounter response =
    case response of
        RemoteData.Success data ->
            div [ class "unread-counter" ]
                [ text ("unread: " ++ toString(data.unread)) ]

        _ ->
            text "no count yet"


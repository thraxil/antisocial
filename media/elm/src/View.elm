module View exposing (..)

import Entries.List
import Html exposing (Html, div, text)
import Html.Attributes exposing (class)
import Models exposing (Model, Entry)
import Msgs exposing (Msg)
import RemoteData exposing (WebData)


view : Model -> Html Msg
view model =
    div []
        [ page model.entries
        , unreadCounter model
        ]


page : WebData (List Entry) -> Html Msg
page response =
    case response of
        RemoteData.NotAsked ->
            text ""

        RemoteData.Loading ->
            text "loading..."

        RemoteData.Success entries ->
            Entries.List.view entries

        RemoteData.Failure error ->
            text (toString error)
                

unreadCounter : Model -> Html Msg
unreadCounter model =
    div [ class "unread-counter" ]
        [ text ("unread: " ++ toString(model.unread)) ]


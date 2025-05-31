import streamlit as st
import sqlite3
import pandas as pd

# Connexion à la base de données SQLite
conn = sqlite3.connect('hotel_db.sqlite')
c = conn.cursor()

# Titre de l'application
st.title("Gestion d'Hôtel")

# Menu latéral
option = st.sidebar.selectbox("Choisir une action", [
    "Liste des Réservations",
    "Clients à Paris",
    "Nombre de Réservations par Client",
    "Chambres Disponibles (entre deux dates)"
])

# a. Liste des Réservations
if option == "Liste des Réservations":
    st.subheader("Liste des Réservations avec Détails")
    query = """
        SELECT R.id_Reservation, R.Date_debut AS Date_Arrivée, R.Date_fin AS Date_Départ,
               C.Nom AS Client, H.Ville AS Ville_Hôtel
        FROM Reservation R
        JOIN Client C ON R.id_Client = C.id_Client
        JOIN Concerner Co ON R.id_Reservation = Co.id_Reservation
        JOIN Chambre Ch ON Co.id_Type = Ch.id_Type
        JOIN Hotel H ON Ch.id_Hotel = H.id_Hotel
    """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)

# b. Clients qui habitent à Paris
elif option == "Clients à Paris":
    st.subheader("Clients résidant à Paris")
    query = "SELECT * FROM Client WHERE Ville = 'Paris'"
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)

# c. Nombre de réservations par client
elif option == "Nombre de Réservations par Client":
    st.subheader("Nombre de Réservations par Client")
    query = """
        SELECT C.id_Client, C.Nom AS Nom_Client, COUNT(R.id_Reservation) AS Nb_Reservations
        FROM Client C
        LEFT JOIN Reservation R ON C.id_Client = R.id_Client
        GROUP BY C.id_Client, C.Nom
    """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)

# d. Nombre de chambres par type
# e. Chambres disponibles entre deux dates
elif option == "Chambres Disponibles (entre deux dates)":
    st.subheader("Chambres Disponibles")
    date_debut = st.date_input("Date de début")
    date_fin = st.date_input("Date de fin")
    if date_debut and date_fin:
        query = """
            SELECT * FROM Chambre 
            WHERE id_Chambre NOT IN (
                SELECT Ch.id_Chambre
                FROM Chambre Ch
                JOIN Concerner Co ON Ch.id_Type = Co.id_Type
                JOIN Reservation R ON Co.id_Reservation = R.id_Reservation
                WHERE R.Date_debut <= ?
                AND R.Date_fin >= ?
            )
        """
        df = pd.read_sql_query(query, conn, params=(date_fin, date_debut))  # Attention à l’ordre des dates
        st.dataframe(df)

# Fermeture de la connexion
conn.close()
using System;
using System.Collections.Generic;

namespace TelemetriaDOC
{
    public class Tracker
    {
        private static Tracker instance = null;
        private Serializer serializer;
        private Persistence persistence;

        private EventQueue eventQueue;

        private Guid sessionID;
        private int gameID;
        private bool isFirstGame;

        private Tracker()
        {
            // Para que los float se escriban siempre con "." en lugar de con ","
            System.Threading.Thread.CurrentThread.CurrentCulture = new System.Globalization.CultureInfo("en-US");
        }

        public static Tracker Instance()
        {
            return instance;
        }

        public static bool Init(Format format, Type type, string name, int sizeQueue)
        {
            if (instance != null)
                return false;

            instance = new Tracker();

            //Iniciar serializador
            instance.InitSerializer(format);

            //Iniciar persistencia
            instance.InitPersistence(type, name);

            instance.eventQueue = new EventQueue(ref instance, sizeQueue);

            instance.sessionID = Guid.NewGuid();
            instance.gameID = 0;
            instance.isFirstGame = true;

            return true;
        }

        public void InitSerializer(Format format)
        {
            switch (format)
            {
                case Format.JSON:
                    instance.serializer = new SerializerJSON();
                    break;
            }
        }

        public void InitPersistence(Type typeSave, string name)
        {
            switch (typeSave)
            {
                case Type.Disk:
                    instance.persistence = new DiskPersistence(name, instance.serializer);
                    break;
            }
        }

        public static void TrackEvent(Event e) 
        {
            e.SetSessionID(instance.sessionID);

            // Si el evento corresponde a un inicio de partida se incrementa el contador gameID
            if (e is GameStateEvent gameStateEvent && gameStateEvent.GetEventType() == GameStateEvent.EventType.GameStart) 
            {
                // En la primera partida no se incrementa el contador para que el gameID sea el mismo
                // que el del evento de inicio de sesion
                if (!instance.isFirstGame) instance.gameID++;
                else instance.isFirstGame = false;
            }

            e.SetGameID(instance.gameID);
            instance.eventQueue.AddEvent(e);
        }

        public void Flush(ref Queue<Event> events)
        {
            string text = "";

            // Serializamos cada evento de la cola
            while(events.Count > 0)
            {
                text += instance.serializer.Serialize(events.Dequeue());
            }

            events.Clear();

            instance.persistence.Write(text);            
        }

        public static void Closing()
        {
            instance.CloseArch();
        }
        private void CloseArch()
        {
            instance.eventQueue.FlushQueue();
            instance.persistence.Write(instance.serializer.SerializerEnding());
            instance.persistence.Close();
        }
    }
}
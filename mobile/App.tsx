import React, { useEffect } from 'react';
import { View, Text, Button } from 'react-native';
import * as Notifications from 'expo-notifications';
import axios from 'axios';

export default function App() {
  const [rides, setRides] = useState([]);
  const { confirmPayment } = useConfirmPayment();

  useEffect(() => {
    axios.get('http://localhost:8000/rides/search?origin=Uptown').then(res => setRides(res.data));
  }, []);

  const bookRide = async (rideId: number) => {
    const { data: { clientSecret } } = await axios.post('http://localhost:8000/bookings', { ride_id: rideId, seats_booked: 1 });
    // Confirm payment (similar to web)
    const { error } = await confirmPayment(clientSecret, { type: 'Card' });
    if (error) alert(error.message);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Neighboride Mobile</Text>
      {rides.map((ride: any) => (
        <View key={ride.id} style={styles.ride}>
          <Text>{ride.origin} → {ride.destination} - ${ride.price_per_seat}</Text>
          <Button title="Book" onPress={() => bookRide(ride.id)} />
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, justifyContent: 'center' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  ride: { padding: 10, borderBottomWidth: 1, marginBottom: 10 }
});

  /**async function registerForPushNotificationsAsync() {
    const { status } = await Notifications.requestPermissionsAsync();
    if (status === 'granted') {
      const token = (await Notifications.getExpoPushTokenAsync()).data;
      axios.post('http://localhost:8000/users/me/push-token', { token });
    }
  }

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Neighboride Mobile</Text>
      
      {/* Rides list as before }
    </View>
  );
}**/
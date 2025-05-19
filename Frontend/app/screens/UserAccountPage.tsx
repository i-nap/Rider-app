import React from 'react';
import { View, Text, StyleSheet, Image, Button, ScrollView } from 'react-native';

const UserAccountPage = () => {
  const handleLogout = () => {
    console.log('User logged out');
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.card}>
        <Image
          style={styles.profileImage}
          source={{ uri: 'https://placehold.co/60x60' }}
        />
        <Text style={styles.userName}>Inap Maharjan</Text>

        <View style={styles.buttonRow}>
          <View style={styles.button}>
            <Text style={styles.buttonText}>Create Circle</Text>
          </View>
          <View style={styles.button}>
            <Text style={styles.buttonText}>Join Circle</Text>
          </View>
        </View>

        <View style={styles.cardBox}>
          <Text style={styles.sectionTitle}>Ride Description</Text>
          <View style={styles.dotRow}>
            <View style={styles.dot} />
            <Text style={styles.dotLabel}>Kms Rode :</Text>
            <Text style={styles.dotValue}>1537 kms</Text>
          </View>
          <View style={styles.dotRow}>
            <View style={styles.dot} />
            <Text style={styles.dotLabel}>Max Speed :</Text>
            <Text style={styles.dotValue}>500 km/h</Text>
          </View>
          <View style={styles.dotRow}>
            <View style={styles.dot} />
            <Text style={styles.dotLabel}>Last Ride :</Text>
            <Text style={styles.dotValue}>23 January 2029</Text>
          </View>
          <View style={styles.dotRow}>
            <View style={styles.dot} />
            <Text style={styles.dotLabel}>Joined :</Text>
            <Text style={styles.dotValue}>1537 circles</Text>
          </View>
        </View>

        <View style={styles.cardBox}>
          <Text style={styles.sectionTitle}>Destination Reached</Text>
          <View style={styles.dotRow}>
            <View style={styles.dot} />
            <Text style={styles.dotLabel}>Badimalika :</Text>
            <Text style={styles.dotValue}>23 January 2029</Text>
          </View>
          <View style={styles.dotRow}>
            <View style={styles.dot} />
            <Text style={styles.dotLabel}>Mustang :</Text>
            <Text style={styles.dotValue}>23 January 2029</Text>
          </View>
          <View style={styles.dotRow}>
            <View style={styles.dot} />
            <Text style={styles.dotLabel}>Pokhara :</Text>
            <Text style={styles.dotValue}>23 January 2029</Text>
          </View>
          <View style={styles.dotRow}>
            <View style={styles.dot} />
            <Text style={styles.dotLabel}>Ghuman :</Text>
            <Text style={styles.dotValue}>23 January 2029</Text>
          </View>
        </View>

      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#F0F8FF',
    alignItems: 'center',
    paddingVertical: 40,
  },
  card: {
    backgroundColor: '#A8BDD0',
    borderRadius: 30,
    width: 320,
    padding: 20,
    alignItems: 'center',
  },
  profileImage: {
    width: 60,
    height: 60,
    borderRadius: 30,
    marginBottom: 10,
  },
  userName: {
    fontSize: 20,
    fontFamily: 'Inter',
    color: '#000000',
    marginBottom: 20,
  },
  buttonRow: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#000000',
    borderRadius: 40,
    paddingVertical: 8,
    paddingHorizontal: 16,
    marginHorizontal: 8,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontFamily: 'Inter',
  },
  cardBox: {
    backgroundColor: '#000000',
    borderRadius: 16,
    width: '100%',
    padding: 16,
    marginBottom: 20,
  },
  sectionTitle: {
    color: '#FFFFFF',
    fontSize: 18,
    fontFamily: 'Inter',
    marginBottom: 10,
  },
  dotRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  dot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: '#D9D9D9',
    marginRight: 8,
  },
  dotLabel: {
    color: '#C1B9B9',
    fontSize: 14,
    fontFamily: 'Inter',
    flex: 1,
  },
  dotValue: {
    color: '#FFFFFF',
    fontSize: 14,
    fontFamily: 'Inter',
  },
});

export default UserAccountPage;

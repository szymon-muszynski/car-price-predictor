import { useState } from 'react';
import axios from 'axios';
import './App.css'; 

interface CarData {
  przebieg: number | '';
  pojemnosc_skokowa: number | '';
  moc: number | '';
  wiek: number | '';
  rodzaj_paliwa: string;
  skrzynia_biegow: string;
  marka: string;
}

function App() {
  const [formData, setFormData] = useState<CarData>({
    przebieg: '',
    pojemnosc_skokowa: '',
    moc: '',
    wiek: '',
    rodzaj_paliwa: 'Benzyna',
    skrzynia_biegow: 'Manualna',
    marka: 'BMW'
  });

  const [predictedPrice, setPredictedPrice] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'number' ? (value === '' ? '' : Number(value)) : value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPredictedPrice(null);

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/predictions/price', formData);
      setPredictedPrice(response.data.predicted_price);
    } catch (err: any) {
      console.error(err);
      setError('Wystąpił błąd podczas łączenia. Upewnij się, że backend działa.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '600px', margin: '0 auto', padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1 style={{ textAlign: 'center', color: '#2c3e50' }}>Wycena Twojego Auta</h1>
      <h1 style={{ textAlign: 'center', color: '#2c3e50' }}>🚗</h1>
      <p style={{ textAlign: 'center', color: '#7f8c8d', marginBottom: '2rem' }}>
        Wprowadź parametry pojazdu, a model oszacuje jego wartość.
      </p>

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        
        <div style={{ display: 'flex', gap: '1rem' }}>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <label>Przebieg (km):</label>
            <input type="number" name="przebieg" value={formData.przebieg} onChange={handleChange} required style={{ padding: '0.5rem' }} />
          </div>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <label>Wiek (lata):</label>
            <input type="number" name="wiek" value={formData.wiek} onChange={handleChange} required style={{ padding: '0.5rem' }} />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <label>Moc (KM):</label>
            <input type="number" name="moc" value={formData.moc} onChange={handleChange} required style={{ padding: '0.5rem' }} />
          </div>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <label>Pojemność (cm³):</label>
            <input type="number" name="pojemnosc_skokowa" value={formData.pojemnosc_skokowa} onChange={handleChange} required style={{ padding: '0.5rem' }} />
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <label>Marka:</label>
          <input 
            type="text" 
            name="marka" 
            value={formData.marka} 
            onChange={handleChange} 
            required 
            placeholder="np. BMW, Toyota, Mercedes-Benz"
            style={{ padding: '0.5rem' }} 
          />
        </div>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <label>Paliwo:</label>
            <select name="rodzaj_paliwa" value={formData.rodzaj_paliwa} onChange={handleChange} style={{ padding: '0.5rem' }}>
              <option value="Benzyna">Benzyna</option>
              <option value="Diesel">Diesel</option>
              <option value="Hybryda">Hybryda</option>
              <option value="Hybryda Plug-in">Hybryda Plug-in</option>
              <option value="Elektryczny">Elektryczny</option>
              <option value="Benzyna+LPG">Benzyna + LPG</option>
            </select>
          </div>
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
            <label>Skrzynia biegów:</label>
            <select name="skrzynia_biegow" value={formData.skrzynia_biegow} onChange={handleChange} style={{ padding: '0.5rem' }}>
              <option value="Manualna">Manualna</option>
              <option value="Automatyczna">Automatyczna</option>
            </select>
          </div>
        </div>

        <button 
          type="submit" 
          disabled={loading}
          style={{
            padding: '1rem',
            backgroundColor: loading ? '#bdc3c7' : '#3498db',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            fontSize: '1.1rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            marginTop: '1rem'
          }}
        >
          {loading ? 'Przeliczanie w macierzach AI...' : 'Wyceń samochód'}
        </button>
      </form>

      {error && (
        <div style={{ marginTop: '2rem', padding: '1rem', backgroundColor: '#ffcccc', color: '#c0392b', borderRadius: '5px' }}>
          {error}
        </div>
      )}

      {predictedPrice !== null && !error && (
        <div style={{ marginTop: '2rem', padding: '1.5rem', backgroundColor: '#e8f8f5', border: '2px solid #2ecc71', borderRadius: '8px', textAlign: 'center' }}>
          <h2 style={{ color: '#27ae60', margin: 0 }}>Szacowana wartość:</h2>
          <h1 style={{ color: '#2c3e50', fontSize: '3rem', margin: '0.5rem 0' }}>
            {predictedPrice.toLocaleString('pl-PL')} PLN
          </h1>
        </div>
      )}
    </div>
  );
}

export default App;
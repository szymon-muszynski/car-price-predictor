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

interface SimilarCar {
  tytul: string;
  cena: number;
  rocznik: number;
  przebieg: number;
  moc: number;
  pojemnosc_skokowa: number;
  url: string;
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
  const [similarCars, setSimilarCars] = useState<SimilarCar[]>([]);
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
    setSimilarCars([]); // <-- Zerujemy listę przed nowym zapytaniem

    try {
      // Wysyłamy dwa zapytania jednocześnie, żeby było szybciej
      const [priceResponse, similarResponse] = await Promise.all([
        axios.post('https://car-price-api-sbfh.onrender.com/api/predictions/price', formData),
        axios.post('https://car-price-api-sbfh.onrender.com/api/predictions/similar', formData)
      ]);
      
      setPredictedPrice(priceResponse.data.predicted_price);
      setSimilarCars(similarResponse.data.similar_cars); // <-- Zapisujemy listę do stanu
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

      {loading && (
        <div style={{ marginTop: '1.5rem', padding: '1rem', backgroundColor: '#fff3cd', color: '#856404', borderRadius: '5px', border: '1px solid #ffeeba', textAlign: 'center', lineHeight: '1.5' }}>
          ⏳ <strong>Uwaga:</strong> Pierwsza wycena może potrwać do 50 sekund, ponieważ nasz darmowy serwer musi się "wybudzić" z uśpienia. <br/>
          Kolejne zapytania będą już błyskawiczne. Proszę o cierpliwość! ☕
        </div>
      )}

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

      {/* NOWA SEKCJA: PODOBNE OFERTY */}
      {similarCars.length > 0 && !error && (
        <div style={{ marginTop: '2rem' }}>
          <h3 style={{ color: '#2c3e50', borderBottom: '2px solid #ecf0f1', paddingBottom: '0.5rem' }}>
            Najbardziej podobne oferty z Otomoto:
          </h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
            {similarCars.map((car, index) => (
              <a 
                key={index} 
                href={car.url} 
                target="_blank" 
                rel="noopener noreferrer"
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  padding: '1.5rem',
                  backgroundColor: 'white',
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  textDecoration: 'none',
                  color: 'inherit',
                  boxShadow: '0 2px 5px rgba(0,0,0,0.05)'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.8rem' }}>
                  <h4 style={{ margin: 0, color: '#2980b9', fontSize: '1.2rem' }}>{car.tytul}</h4>
                  <span style={{ fontWeight: 'bold', fontSize: '1.3rem', color: '#e67e22' }}>
                    {car.cena.toLocaleString('pl-PL')} PLN
                  </span>
                </div>
                
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: '1.5rem', color: '#7f8c8d', fontSize: '1rem' }}>
                  <span>Rok: <br /> {car.rocznik}</span>
                  <span>Przebieg: <br /> {car.przebieg.toLocaleString('pl-PL')} km</span>
                  <span>Moc: <br /> {car.moc} KM</span>
                  <span>Pojemność: <br /> {car.pojemnosc_skokowa} cm³</span>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}

export default App;
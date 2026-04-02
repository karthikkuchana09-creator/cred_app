import { useEffect, useState } from 'react';
import { fetchCards, addCard, deleteCard } from '../services/cardService';

export default function CardManager() {
  const [cards, setCards] = useState([]);
  const [rawNumber, setRawNumber] = useState('');

  const loadCards = async () => {
    const res = await fetchCards();
    setCards(res.data);
  };

  useEffect(() => {
    loadCards();
  }, []);

  const handleAdd = async () => {
    if (!rawNumber) return;
    await addCard({ raw_number: rawNumber, card_type: 'VISA' });
    setRawNumber('');
    loadCards();
  };

  const handleDelete = async (id) => {
    await deleteCard(id);
    loadCards();
  };

  return (
    <div>
      <h3>Card Management</h3>
      <input value={rawNumber} onChange={(e) => setRawNumber(e.target.value)} placeholder="Card number" />
      <button onClick={handleAdd}>Add Card</button>
      <ul>
        {cards.map((card) => (
          <li key={card.id}>
            {card.masked_number} - {card.card_type}
            <button onClick={() => handleDelete(card.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

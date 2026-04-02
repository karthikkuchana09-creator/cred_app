import { useEffect, useState } from 'react';
import { fetchTransactions } from '../services/transactionService';
import { makePayment } from '../services/paymentService';

export default function Payment() {
  const [transactions, setTransactions] = useState([]);
  const [userEmail, setUserEmail] = useState('email@domain.com');
  const [cardLast4, setCardLast4] = useState('****');
  const [amount, setAmount] = useState(1);

  const loadTransactions = async () => {
    const res = await fetchTransactions();
    setTransactions(res.data);
  };

  useEffect(() => {
    loadTransactions();
  }, []);

  const handlePayment = async () => {
    await makePayment({ user_email: userEmail, card_last4: cardLast4, amount });
    setAmount(1);
    loadTransactions();
  };

  return (
    <div>
      <h3>Payment</h3>
      <p>
        Email: <input value={userEmail} onChange={(e) => setUserEmail(e.target.value)} />
      </p>
      <p>
        Card last4: <input value={cardLast4} onChange={(e) => setCardLast4(e.target.value)} maxLength={4} />
      </p>
      <p>
        Amount: <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} />
      </p>
      <button onClick={handlePayment}>Make Payment</button>
      <h4>History</h4>
      <ul>
        {transactions.map((t) => (
          <li key={t.id}>{t.id}: {t.amount} ({t.status})</li>
        ))}
      </ul>
    </div>
  );
}

# Strategy

## What is Arbitrage

The goal here is to use **arbitrage**, which is when the same asset is worth different values at different exchanges. This is the method behind much of high frequency trading, when traders can buy low and sell high instantly. As traders capitalize on arbitrage, it closes up. Usually in the real world this happens in the range of microseconds. With most cryptocurrencies, it can be up to a couple hours.

Bitcoin is a bit tricky. In order to make a transaction, you have to request verification from 3-6 anonymous sources in the Bitcoin network. This involves solving a computationally hard problem. So you can buy a coin, and it won't be actually verified until 15-30 minutes afterwards. Many exchanges have even longer verification times, up to an hour. This makes arbitrage tricky, since trading between exchanges involves buying in one market, transferring funds, and then buying in another market.

The goal is to eliminate having to wait for transactions to be verified. To that end, we use the following fundamental principle of arbitrage: the market price of an asset will converge. No matter what happens, we assume that this will eventually come to be true in all cases. However, it might not. For example, when an exchange fails, prices diverge forever. We have to be careful not to lose all of our money in that case. A second fundamental principle of our strategy is that Bitcoin will remain relatively stable. We will buy other assets with Bitcoins, so we need to be fairly confident that the price of Bitcoin will not fluctuate too much in between the time that an arbitrage opens up (we _enter_ the market) and when the arbitrage closes up (we _exit_ the market).

## Types of Orders, Buying and Selling Short

The two main techniques we will use are buying long and selling short. Buying long is your regular old buying stocks. Selling short is essentially the process of selling assets you don't have (from a loan), and then buying them back at a lower price, pocketing the profit. Note that you can theoretically lose an unlimited amount of money by selling short, as the price can increase quite a bit after you sell your asset, and you can be left with debts you cannot possibly pay.

Note that there are different types of orders you can place on a stock market. A common type of order is a limit order, which is of the form: Buy/Sell when the price hits below/above X BTC. This usually has the lowest fees. This is called a **maker** fee.

Supppose on the other hand, you make a request that is likely to be fulfilled immediately. Suppose Bitcoin is selling at $4000, and you want to buy it at $4000; then you are basically removing a request from the book immediately. This is called a **taker** fee and it is usually higher. This is the kind of deal you have to make in arbitrage; you want to buy/sell immediately.

## A Strategy That Reduces Risk

As mentioned before, we assume that the market will converge to a single price. Suppose we start with a situation where an asset is worth more in exchange A than in exchange B. Then we assume that the two prices will meet somewhere soon in the future. This could happen in one of five cases.

- The price in A increases, and B increases as well.
- The price in A stays the same, B increases to match it.
- The price in A decreases, and B increases to match it.
- The price in A decreases, and B stays the same.
- The price in A decreases, and B decreases as well.

Each of these scenarios leads to slightly different fee structures. But the strategy is always the same:

**In the lower market, buy long; in the higher market, sell short. When the markets converge, sell what you bought and buy back what you sold**.

Do the results on paper, and you'll see that you make a profit (up to a fee) every time. For example, take the second scenario. We bought B, and sell it later at a higher price -- so we make a profit. Take the first scenario. We lose money by buying A, but gain more money by selling B, so in the end we make a profit.

A key thing here is that we have to be reasonably sure that the decision that we make will indeed make a profit that is larger than any fees we will have to pay. We are essentially always making 2-4 transactions, on each of which we will pay a taker fee of 0.1-0.3%. So we won't always make a profit on every single arbitrage, of course. But if the initial spread is large enough, and the prices end up converging closely enough, the differential there is enough to make a profit. 

## What Trade To Make: Predicting Profits

We can predict profits by looking at what a typical arbitrage looks like. In every historical arbitrage situation (or a large amount of them), we will try our strategy and see if it makes a profit that counterbalances the fees we will have to pay. Then hopefully we'll be able to pick deals that are profitable for us. Furthermore, we want to train our bot to look out for a certain % spread that is both frequent in the real data and profitable.

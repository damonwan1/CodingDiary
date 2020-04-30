### Pair用法？
* 在核心Java库中可以使用配对(Pair)的实现，配对(Pair)。配对提供了一种方便方式来处理简单的键值关联，场景：
  * 想要返回两个值，两个值都很有用的时候；
  * HashMap的Key想用两个值的时候；
  * 既要**以键值对的方式存储数据列表**，同时在输出时**保持顺序**的情况下，我们可以使用 Pair 搭配 ArrayList 实现
  *记录推送过来的消息，我们可以用 Pair 的 first 记录消息到达的时间戳，second 记录消息体。
  ``` Java
  ArrayList<Pair<Long,Message>> dataList = new ArrayList();
  ```
 
### 源码
``` Java
public class Pair<F, S> {
    public final F first;
    public final S second;

    public Pair(F first, S second) {
        this.first = first;
        this.second = second;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Pair)) {
            return false;
        }
        Pair<?, ?> p = (Pair<?, ?>) o;
        return Objects.equals(p.first, first) && Objects.equals(p.second, second);
    }

    // ...

    public static <A, B> Pair <A, B> create(A a, B b) {
        return new Pair<A, B>(a, b);
    }
}
```
* 可以看到 equals方法比的是值，也就是说只要两个Pair对象的**first、second相同**，那么他们就equals返回true
------
### 使用方式
``` Java
// 两种方式都可以创建 Pair 实例，而第二种方式内部实际上也是使用第一种方式创建
Pair pair1 = new Pair<Integer, String>(1, "111"); // 第一种方式创建
Pair pair2 = Pair.create(1, 111); // 第二种方式创建
Pair pair3 = Pair.create(1, 111);

Log.e(TAG, pair1.first.toString()); // 1
Log.e(TAG, pair1.second.toString()); // 111
Log.e(TAG, pair1.second.equals("111") + ""); // true
Log.e(TAG, pair1.second.equals(111) + ""); // false

Log.e(TAG, pair1.equals(pair2) + ""); // false
Log.e(TAG, pair2.equals(pair3) + ""); // true
```

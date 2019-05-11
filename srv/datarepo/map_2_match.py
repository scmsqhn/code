#include <bits/stdc++.h>
    using namespace std;
     
    int n, m;//n代表图的点数， m代表边数
    int len;//用来记录一条增广路径
    const int maxn_node = 1e2+5;
    bool mp[maxn_node][maxn_node];//记录图的连通性
    bool book[maxn_node];//从每个节点遍历是看是否经过，记住在遍历的开始一定要设置初始点为已遍历对象，否则会出现首位相接的错误
    int match[maxn_node];//匹配的边
    vector<int> record;//记录一条可能是增广路径的路径其中有的元素被记录了两次，因此不是最终的路径
    int path[maxn_node];//record路径的筛选形成可判断的路径
     
    bool dfs(int u){
        for(int i=1; i<=n; i++){
            if (i == u) continue;
            if(!book[i] && mp[u][i]){
                book[i] = true;//表示改点已经被经过了，为dfs()创造条件
                if(match[i] == 0 || dfs(i)){//dfs()终止的条件是找到首位都为0的一条路径
                    record.push_back(i);
                    record.push_back(u);
                    return true;
                }
            }
        }
        return false;
    }
    void reverse_connection(){//反转连通的边，使路径数量加一
        for(int i=0; i<len-1; i += 2){
            match[path[i]] = path[i+1];
            match[path[i+1]] = path[i];
        }
        return;
    }
     
    bool is_cross(){//判断是否是合法的增广路径，因为dfs()仅仅记录首尾match[]=0的链，不保证中间是交替链
        if(len == 2){
            return true;
        }
        for(int i=1; i<len-1; i+=2){//首尾无需判断，因为match都是0，中间的点两两进行判断
            if(match[path[i]]!=path[i+1]||match[path[i+1]] != path[i]){//这个一开始里面的判断条件出错了，好坑啊
                return false;
            }
        }
        return true;
    }
     
    int main()
    {
        cin>>n>>m;
        int ans = 0;
        
        //读入图的数据：
        for(int i=0; i<m; i++){
            int from, to;
            cin>>from>>to;
            mp[from][to] = true;
            mp[to][from] = true;
        }
        
        //从每个点开始遍历
        for(int i=1; i<=n; i++){
            for(int j=1; j<=n; j++){//每个点遍历的时候都要将book[]重置一遍
                book[j] = false;
            }
            record.clear();//清空之前记录的路径
            book[i] = true;//一开始的时候一定要初始化,嗯这是我之前提出的注意事项，在此再次提醒自己，否则会形成首尾相同的路径
            if(!match[i] && dfs(i)){//关键是找record
                ;
            }
            if(record.size()>=2){
                //简化record,因为有的点被记录了两次，并且将最终的结果保存在path[]中
                len = 0;
                path[len++] = record[record.size()-1];
                for(int i=record.size()-2; i>=1; i -= 2){
                    path[len++] = record[i];
                }
                path[len++] = record[0];
     
     
                if(is_cross()){//判断是否是合法的增广路径
                    if(len == 2){
                        match[path[0]] = path[1];
                        match[path[1]] = path[0];
                    }
                    ans++;//若是合法的增广路径,条数加一
                }
                else{//不是合法的增广路径，后面就不用翻转边了
                    continue;
                }
                if(len>2){//都走到这一步了，当然是合法的增广路径，翻转边。
                    reverse_connection();
                }
            }
        }
        //输出最终的路径，可能有多组解，但是只能解出一组解
        for(int i=1; i<=n; i++){
            if (match[i] && i<match[i]){
                cout<<i<<"<--------->"<<match[i]<<endl;
            }
        }
        cout<<"max number:"<<ans<<endl;//输出最大的组数
        return 0;
    }


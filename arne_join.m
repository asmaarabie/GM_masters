%function mc1=join(mc,pInit,pTrans);%connects MarkovChain array elements to form a single MarkovChain%with nStates= sum of nStates in all input MarkovChains.%Input MarkovChain elements should have FINITE duration,%because the transition to another MarkovChain can happen only from the EXIT state%of one MarkovChain to the initial states of the following MarkovChain.%%Input:%mc=        array of finite-duration MarkovChain objects%pInit=     initial probability vector%           pInit(i)= prob of entering mc(i) at start.%pTrans=    transition probability matrix between HMMtied elements%           pTrans(i,j)=P( transition from mc(i) exit to mc(j) initial state )%NOTE:  mc is indexed as a column vector, regardless of actual shape.%%Result:%mc1=       new single MarkovChain%           can be finite- or infinite- duration,%           depending on the given pTrans matrix.%firstState=vector with state indices in mc1, corresponding to first state in each mc(:)%           States 1:N_k in mc(k) are mapped to firstState(k):firstState(k+1)-1 in mc1%%Arne Leijon 2009-07-29 tested%               2012-03-06 return vector firstState for external usefunction [mc1,firstState]=join(mc,pInit,pTrans)if length(pInit)~=size(pTrans,1)    error('Incompatible Initial and Transition Prob. size');endif length(pInit)~=numel(mc)    error('Incompatible MarkovChain array size');end;%make sure pInit and pTrans are proper probability matrices:pInit=pInit./repmat(sum(pInit),size(pInit));%normalizepTrans=pTrans./repmat(sum(pTrans,2),1,size(pTrans,2));%normalizenStates=zeros(numel(mc),1);%store input mc nStatesfor i=1:numel(mc)    nStates(i)=mc(i).nStates;end;%firstState(i)=mc1 state index for mc(i) state 1%lastState(i)=mc1 state index for mc(i) last statelastState=cumsum(nStates);%state nr in output mc1firstState=[1;1+lastState(1:end-1)];nStates1=sum(nStates);pI=sparse(nStates1,1);%output initial probability%output transition prob:if size(pTrans,2)>size(pTrans,1) && any(pTrans(:,size(pTrans,1)+1)~=0)    pT=sparse(nStates1,nStates1+1);%finite durationelse    pT=sparse(nStates1,nStates1);%infinite durationend;for i=1:numel(mc)%collect initial prob.s    pI(firstState(i):lastState(i))=mc(i).InitialProb;end;for i=1:numel(mc)%get transition prob.s     A=mc(i).TransitionProb;    pT(firstState(i):lastState(i),firstState(i):lastState(i))=A(1:end,1:nStates(i));%square part    if size(A,2)>size(A,1)%should have EXIT state for join to make sense        for j=1:numel(mc)%transition into first state of mc(j)            pExit=A(:,nStates(i)+1)*pI(firstState(j):lastState(j))';            pT(firstState(i):lastState(i),firstState(j):lastState(j))=...                pT(firstState(i):lastState(i),firstState(j):lastState(j))+pTrans(i,j)*pExit;        end;    else        warning('MarkovChain:join',['No exit from input MarkovChain nr ',int2str(i)]);    end;    if size(pT,2)>size(pT,1)%set transitions to global EXIT state nr nStates1+1        pT(firstState(i):lastState(i),nStates1+1)=pTrans(i,numel(mc)+1)*A(:,nStates(i)+1);%EXIT state    end;end;for i=1:numel(mc)%scale output initial prob.s    pI(firstState(i):lastState(i))=pInit(i)*pI(firstState(i):lastState(i));end;%mc1=MarkovChain(pI,pT);%DONEmc1=mc(1);%just to give it the correct classmc1.InitialProb=pI;mc1.TransitionProb=pT;
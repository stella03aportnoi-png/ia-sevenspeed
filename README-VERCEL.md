# IA Oficial Escuderia Seven — versão Vercel

Esta versão foi criada em uma branch separada para preservar o aplicativo Streamlit original.

## Tecnologias
- React + Vite (interface)
- Vercel Functions (API)
- Google Gemini 2.5 Flash
- Supabase Auth (e-mail/senha e Google OAuth)
- Supabase Postgres (histórico por usuário)

## 1. Criar o banco no Supabase
1. Crie um projeto em https://supabase.com/.
2. Abra SQL Editor e execute todo o conteúdo de `supabase/schema.sql`.
3. Em Authentication → URL Configuration, adicione o domínio da Vercel em Site URL e Redirect URLs (inclua também `http://localhost:5173/**` para testes locais).

## 2. Ativar login Google
Em Supabase → Authentication → Providers → Google, habilite o provedor e informe o OAuth Client ID e Client Secret criados no Google Cloud Console. Configure o callback URL mostrado pelo Supabase no Google Cloud.

## 3. Variáveis de ambiente
Configure em Vercel → Project → Settings → Environment Variables:

- `VITE_SUPABASE_URL`: Project URL do Supabase.
- `VITE_SUPABASE_ANON_KEY`: chave anon/public do Supabase.
- `SUPABASE_URL`: Project URL do Supabase (API).
- `SUPABASE_ANON_KEY`: chave anon/public do Supabase (API).
- `GEMINI_API_KEY`: chave da API Gemini.

Nunca coloque a chave Gemini no frontend nem no GitHub.

## 4. Publicar na Vercel
1. Importe o repositório `stella03aportnoi-png/ia-sevenspeed` na Vercel.
2. Selecione a branch `vercel-version`.
3. Framework preset: Vite. Build command: `npm run build`. Output directory: `dist`.
4. Adicione as variáveis acima e faça Deploy.

## 5. Testes obrigatórios
- Criar conta por e-mail, confirmar e-mail e entrar.
- Entrar com Google após configurar OAuth.
- Criar duas conversas, trocar entre elas, atualizar a página e confirmar que o histórico persiste.
- Confirmar que um usuário não consegue consultar conversas de outro.
- Enviar perguntas sobre regulamentos e verificar as citações de artigos.

## Observações
- A aplicação Streamlit na branch `main` não foi modificada.
- A base `regras.txt` é carregada do branch principal do GitHub.
- O histórico fica associado ao usuário autenticado e protegido por Row Level Security (RLS).
- Esta implementação precisa ser configurada no Supabase e implantada/testada na Vercel antes de estar disponível publicamente.
